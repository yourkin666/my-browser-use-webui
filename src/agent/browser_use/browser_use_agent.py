from __future__ import annotations

import asyncio
import logging
import os
from typing import Optional, List

# from lmnr.sdk.decorators import observe
from browser_use.agent.gif import create_history_gif
from browser_use.agent.service import Agent, AgentHookFunc
from browser_use.agent.views import (
    ActionResult,
    AgentHistory,
    AgentHistoryList,
    AgentStepInfo,
    ToolCallingMethod,
)
from browser_use.browser.views import BrowserStateHistory
from browser_use.utils import time_execution_async
from dotenv import load_dotenv
from browser_use.agent.message_manager.utils import is_model_without_tool_support

load_dotenv()
logger = logging.getLogger(__name__)

SKIP_LLM_API_KEY_VERIFICATION = (
        os.environ.get("SKIP_LLM_API_KEY_VERIFICATION", "false").lower()[0] in "ty1"
)


class BrowserUseAgent(Agent):
    def __init__(self, *args, **kwargs):
        # Dynamically scan for image files in downloads directory
        file_paths = []
        downloads_dir = os.path.abspath("./tmp/downloads")
        
        if os.path.exists(downloads_dir):
            logger.info(f"Scanning for image files in: {downloads_dir}")
            for file in os.listdir(downloads_dir):
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.svg', '.tiff', '.tif')):
                    file_path = os.path.join(downloads_dir, file)
                    file_paths.append(file_path)
                    logger.info(f"Found image file: {file}")
        else:
            logger.warning(f"Downloads directory not found: {downloads_dir}")
            os.makedirs(downloads_dir, exist_ok=True)
            logger.info(f"Created downloads directory: {downloads_dir}")
        
        # Set available_file_paths parameter
        kwargs['available_file_paths'] = file_paths
        
        # Call parent constructor
        super().__init__(*args, **kwargs)
        
        logger.info(f"BrowserUseAgent initialized with {len(file_paths)} available image files:")
        for path in file_paths:
            file_size = os.path.getsize(path) / (1024 * 1024)  # Size in MB
            logger.info(f"  ✅ {os.path.basename(path)} ({file_size:.1f}MB)")
        
        if not file_paths:
            logger.warning("⚠️ No image files found in downloads directory. You may need to place image files there before uploading.")

    def _set_tool_calling_method(self) -> ToolCallingMethod | None:
        tool_calling_method = self.settings.tool_calling_method
        if tool_calling_method == 'auto':
            if is_model_without_tool_support(self.model_name):
                return 'raw'
            elif self.chat_model_library == 'ChatGoogleGenerativeAI':
                return None
            elif self.chat_model_library == 'ChatOpenAI':
                return 'function_calling'
            elif self.chat_model_library == 'AzureChatOpenAI':
                return 'function_calling'
            else:
                return None
        else:
            return tool_calling_method

    @time_execution_async("--run (agent)")
    async def run(
            self, max_steps: int = 100, on_step_start: AgentHookFunc | None = None,
            on_step_end: AgentHookFunc | None = None
    ) -> AgentHistoryList:
        """Execute the task with maximum number of steps"""

        loop = asyncio.get_event_loop()

        # Set up the Ctrl+C signal handler with callbacks specific to this agent
        from browser_use.utils import SignalHandler

        signal_handler = SignalHandler(
            loop=loop,
            pause_callback=self.pause,
            resume_callback=self.resume,
            custom_exit_callback=None,  # No special cleanup needed on forced exit
            exit_on_second_int=True,
        )
        signal_handler.register()

        try:
            self._log_agent_run()

            # Execute initial actions if provided
            if self.initial_actions:
                result = await self.multi_act(self.initial_actions, check_for_new_elements=False)
                self.state.last_result = result

            for step in range(max_steps):
                # Check if waiting for user input after Ctrl+C
                if self.state.paused:
                    signal_handler.wait_for_resume()
                    signal_handler.reset()

                # Check if we should stop due to too many failures
                if self.state.consecutive_failures >= self.settings.max_failures:
                    logger.error(f'❌ Stopping due to {self.settings.max_failures} consecutive failures')
                    break

                # Check control flags before each step
                if self.state.stopped:
                    logger.info('Agent stopped')
                    break

                while self.state.paused:
                    await asyncio.sleep(0.2)  # Small delay to prevent CPU spinning
                    if self.state.stopped:  # Allow stopping while paused
                        break

                if on_step_start is not None:
                    await on_step_start(self)

                step_info = AgentStepInfo(step_number=step, max_steps=max_steps)
                await self.step(step_info)

                if on_step_end is not None:
                    await on_step_end(self)

                if self.state.history.is_done():
                    if self.settings.validate_output and step < max_steps - 1:
                        if not await self._validate_output():
                            continue

                    await self.log_completion()
                    break
            else:
                error_message = 'Failed to complete task in maximum steps'

                self.state.history.history.append(
                    AgentHistory(
                        model_output=None,
                        result=[ActionResult(error=error_message, include_in_memory=True)],
                        state=BrowserStateHistory(
                            url='',
                            title='',
                            tabs=[],
                            interacted_element=[],
                            screenshot=None,
                        ),
                        metadata=None,
                    )
                )

                logger.info(f'❌ {error_message}')

            return self.state.history

        except KeyboardInterrupt:
            # Already handled by our signal handler, but catch any direct KeyboardInterrupt as well
            logger.info('Got KeyboardInterrupt during execution, returning current history')
            return self.state.history

        finally:
            # Unregister signal handlers before cleanup
            signal_handler.unregister()

            if self.settings.save_playwright_script_path:
                logger.info(
                    f'Agent run finished. Attempting to save Playwright script to: {self.settings.save_playwright_script_path}'
                )
                try:
                    # Extract sensitive data keys if sensitive_data is provided
                    keys = list(self.sensitive_data.keys()) if self.sensitive_data else None
                    # Pass browser and context config to the saving method
                    self.state.history.save_as_playwright_script(
                        self.settings.save_playwright_script_path,
                        sensitive_data_keys=keys,
                        browser_config=self.browser.config,
                        context_config=self.browser_context.config,
                    )
                except Exception as script_gen_err:
                    # Log any error during script generation/saving
                    logger.error(f'Failed to save Playwright script: {script_gen_err}', exc_info=True)

            await self.close()

            if self.settings.generate_gif:
                output_path: str = 'agent_history.gif'
                if isinstance(self.settings.generate_gif, str):
                    output_path = self.settings.generate_gif

                create_history_gif(task=self.task, history=self.state.history, output_path=output_path)
