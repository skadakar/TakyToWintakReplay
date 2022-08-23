#### TakyToWintakReplay
Script to turn [Taky](https://github.com/tkuester/taky) COT logs into a database for WinTAK Replay function.

You must have `cot_log` set to `true` and a log path specified to get the logs required for this to work. 

The script expects to find the logs under `./logs`.

Run the script and find the output `cpr` file. Import into WinTAK to replay

#### Limitations:
* Any GeoChat will be discarded.
* Any event before 2005 will be discarded.
* It's extremely poorly written.
