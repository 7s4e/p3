# import pytest
# from menu import Menu


# # @pytest.fixture
# # def mock_run(mocker):
# #     return mocker.patch("commands.sub.run")


# # Test runCommand
# # @pytest.mark.parametrize(
# #     "command, capture_output, mock_return, exp_output, should_raise",
# #     [
# #         # Test case 1: Command success with output.
# #         (
# #             "echo 'No Capture'", 
# #             False, 
# #             {"returncode": 0}, 
# #             None, 
# #             False
# #         )
# #     ]
# # )
# # def test_run_command(mocker, mock_run, command, mock_return, capture_output, 
# #                      exp_output, should_raise):
# #     # Setup
# #     mock_run.return_value = mocker.MagicMock(**mock_return)

# #     # Execute
# #     if should_raise:
# #         with pytest.raises(RuntimeError, match=mock_return.get("stderr", "")):
# #             cmd.run_command(command, capture_output, use_shell=True)
# #     else:
# #         result = cmd.run_command(command, capture_output, use_shell=True)
        
# #         # Verify method output
# #         assert result == exp_output
    
# #     # Verify method process
# #     mock_run.assert_called_once_with(command, capture_output=capture_output, 
# #                                      shell=True, text=True, 
# #                                      stdout=sys.stdout 
# #                                      if not capture_output else None,
# #                                      stderr=sys.stderr 
# #                                      if not capture_output else None)

