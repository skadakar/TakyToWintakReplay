#### TakyToWintakReplay
Script to turn [Taky](https://github.com/tkuester/taky) COT logs into a database for WinTAK Replay function.

You must have `cot_log` set to `true` and a `log_cot` path specified to get the logs required for this to work. 

This outputs .COT files in the log directory, which can be parsed into a `cpr` database wintak can replay. 

The script expects to find the logs under `./logs`.

#### Limitations:
* Any GeoChat will be discarded.
* Any event before 2005 will be discarded.
* The word poop is mentioned four times in the source.. 
