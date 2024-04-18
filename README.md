# Simple Timemachine

## Motivation

- When playing Neofly in Microsoft Flight Simulator, the Neofly app saves the progress to one file only and replace the old one. I want to have a history of saved files, in case I need to restart the progress after crashing the plane.
- I was able to do it manually (by renaming the file), but why not to have an automated agent that can copy the file to a backup location and rename it, according to timestamp

## Technical Proposal - MVP

1. Agent will be able to monitor a `folder` for a `specific file pattern`. When there is a `new file` (eg file that was not backuped yet), it creates a copy of that file in a `backup folder` with a new name, created as `orig_file_name_without_ext_YYYYMMDD_HHMMSS.orig_extension`
2. In order to keep the load on the system low, it should check new files only every `sleep_time` seconds
3. Configurable items
   - monitored_folder
   - monitored_extension
   - backup_folder
   - sleep_time

## Nice to have

1. Logging to the log file (no more debug prints)
2. The configuration will be done through json file
3. The name of config file or the section in the file can be parametrized through cmdline
4. All configuration parameters through cmdline
5. Agent will monitor several folders

