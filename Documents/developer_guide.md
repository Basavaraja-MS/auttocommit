SVN AUTO COMMIT DEVELOPER GUIDE

-------------------------------

------------------------------



This developer guide gives information about "autocommit" tool internals,

For usage of "autocommit" refer user guide on the same path.





autocommit operations are broadly classified as below 



 * Gather and verify user data

 * Initalize autocommit environment

 * Monitor data modifcation

 * svn operations





Gather and verify user data

---------------------------

* autocommit is designed with the intention of command line interface but nothing to stop

it to utilize as a library.



* For CLI "argparse" library help is taken, where it eases the framing user commands in

user-friendly and less error-prone.



* "get_user_args()" Gives constructed way of user inputs, the obtained user data is used

to overwrite default arguments data

	* Function parameters: None

	* Return value: object with data parameters and there values

	* Extension: For adding new parameters invoke "phrase.add_argument" function,



* "default_command_init()" Provides default arguments for the tool, If there is no additional

parameters provided in the CLI interface these values will be set. 

	* Function parameters: None

	* Return value: Dictnory with default parameters 

	* Extension: Add new dictnory value for future parameters 

* "set_user_args(usr_cmds, deflt_cmds)" sets usr_cmds dictory values to deflt_cmds values and

returns deflt_cmds dictinory. If there is no user commands it returns default parameter values

	* Function parameters: usr_cmds - CLI input values, deflt_cmds - default parameters

	* Return value: updated default value dictionary 

* "args_sanity_check(commands)" Sanity check of command parametres. which makes belwo test cases

	> checks given local path

	> checks given svn path 

	> check boolean vlaues of ignore, force and recursive

	* Function parameters: dictnory of user parameters 

	* Return value: None 

	* Extension: None



Initialize environment

----------------------

* Once all the input values are verified initiate the svn application initialization



* "svn_app_init(commands)" If there is no version controlled directory exists in the user mentioned

local path checkout the svn server path, if its exists updated existing path for new changes.It also

updates the ignore file extensions which should not come under version control 

	* Function parameters: dictnory of user parameters

	* Return value: None

	* Extensaion : Nonea



Monitor data modifcation

------------------------



* "watchdogHandler()" Main constructor class of the watchdog library. For every modification in the local

directory, there is an event will be triggered and according to the defined event respective event handlers

will be invoked. 

There are multiple configuration parameters for "watchdogHandler" constructors which are defined at initial

zation time itself such as,

	>_patterns - File patterns which are only needed to be observed, 'None' makes all file patterns on consideration

        >_ignore_patterns - List of file patterns need to ignore from observation 

        >_case_sensitive -

        >_ignore_directories - Ignores directory modification events

	* Class parameters: As same as above

	* Return value: event handler object which needs to pass in schedule

	* Extention: None



* "observer.schedule" Creates a thread of event handler and waits for events to trigger

	* Function parameters: object of  "watchdogHandler()", user path and recursive switch value (true or false)

	* Return value: None

	* Extension: None



* "observer.start()" Iniatis thread running for scheduler and waits for events

	* Function parameters: None

	* Return value: None

	* Extension: None



NOTE: "command["SLEEP"]": user can utilize sleep parameter to watch events for every "sleep" intervals. Increase

in the sleep time reduces CPU overhead 



svn operations

--------------



* svn_checkin(source_path): Chekin the version controlled path content with host and OS name stamp in the commit message

	* Assumption: Already in version controlled local path 

	* Function parameters: File path for which event is triggerd

	* Return value: None

	* Extension:



* svn_add(src_path): Add newly formed file and directories into version control 

        * Assumption: Already in version controlled local path

        * Function parameters: File path for which event is triggerd

        * Return value: None

        * Extension:



* svn_remove(src_path): Removes deleted file form version control

        * Assumption: Already in version controlled local path

        * Function parameters: File path for which event is triggerd

        * Return value: None

        * Extension:



* svn_checkout(src_path): Checkout user specified host path

        * Assumption: Entered into user specified local path 

        * Function parameters: File path for which event is triggered

        * Return value: None

        * Extension:



* svn_up(command): Copies and rewrites the local changes from the svn server contents

        * Assumption: Already in version controlled local path

        * Function parameters: "command" dictionary 

        * Return value: None

        * Extension: Implement conflict handling 



* svn_ignore(command): Ignores the specified file extensions to come under version control 

        * Assumption: Already in version controlled local path

        * Function parameters: "command" dictionary

        * Return value: None

        * Extension:
