# bpl is a minimalist code generation framework

It's opinionated and insists on being simple. Real simple. 

Mostly what it does is replace strings with other strings, in file and directory names, and within files themselves. 

It is extensible, it can be extended in ways that will make it complicated. You have to do it in C++, but it is all set up for it, and there's not much too it.

**It takes as inputs:**

1. The folder containing the file templates.
2. A mapping of names to values (either as an argument or as a configufation file).
3. A target folder where the new code project is to be generated.
4. A few other runtime configuration parameters:
    1. *strict* means that errors are reported when a replacement is not found and bpl thinks it should be.
    2. *files to ignore* is a list of files, paths, or wildcards whose contents will not be parsed.
    3. *extension to ignore* is a list of files, paths, or wildcards whose contents will not be parsed.

It then traverses the source template, replacing names with values (there's rules, see below) where they are found, and generates new files in the target folder. 

In file names you mark the values to be replaces by double underscores (like **\_\_name__**), in files by double braces (like **{{name}}**). 

There's some functions and some special file names that you can use for special stuff (well, one of each at the time of writing, to create guids and to pull stuff from github on the fly). 

There's an `examples` folder too, if you prefer learning by reading code.

That's pretty much it really - the rest is just a few bells and whistles, and some disambiguation rules. 

## GUI

There's also a little gui to make it easier to use. You need to have python 3 installed for it to work, but not much else. Run blp_gui.sh on linux or blp_gui.bat on windows. 

You can configure visuals in blp_gui.ini file, and run it with -h command line option for help.


## The replacement rules

1.  There is a mapping in the input of names to values. This is just a table of strings.
2.  Names in the mapping are not case sensitive, values are case sensitive.
3.  You can control the case of replacements by how you capitalise the names.
    Say, it there is a mapping defined: name -> Value, then:

        {{name}} or __name__ is replaced by value
        {{NAME}} or __NAME__ is replaced by VALUE
        {{Name}} or __Name__ is replaced by Value
    
    Formally, whenever a name is being replaced by a value:
    - if the name is spelled all in lowercase in the source, it is replaced by the lowercase version if the value in the target.
    - else if the name is spelled all in uppercase in the source, it is replaced by the uppercase version of the value in the target.
    - otherwise it is replaces by the value as it appears in the input map.
    
6.  In file and directory names:
    - names to be replaced are delimeted by two underscores either side of it (like **\_\_name__**).
    - if a name is not found in the map, nothing happens, no errors are thrown. (there is a strict mode of running that makes this an error, if you really want to).
    - there are no escape characters for file and directory name replacements.

7.  In the files' content:
    - names to be replaced are delimeted by two curly braces either side of it (like **{{name}}**).
    - if a name is not found in the map, nothing happens, no errors are thrown. (there is a strict mode of running that makes this an error, if you really want to).
    - whitespace surrounding names in the braces is eaten.
    - nesting is not allowed (e.g. you can't do silly things like {{name1{{name2}}name3}}, it's rude to expect people to be able to read that).
    - you can escape replacement by putting it in double braces (e.g. {{{{don't touch this}}}} evaluates to {{don't touch this}}).
    - there's no messing with escaping, like if you want to do it, you need it open and closed with four braces.

8.  There is a (very) small number of functions that can be used to generate special things. 
    - they are hardcoded, to add one you gotta write some c++.
    - they cannot be used in maps, you just specify that they should be used in the source files, but their arguments can come from the map.
    - they cannot be used in file and directory name substitution; the syntax becomes too complicated.
    - their syntax is name(arg0, arg1, ... , arg5), the name is not case sensitive.
    - an arguments can be an integer, a double, a string (quoted), or a name from the map (not quoted, and case rules work the same).

    **Available functions**:
    - **GUID(int)** - this is because Visual Studio uses guids to link its internal files and configurations. 
    The argument is an identifier of the particular guid: GUID(0) is always the same GUID during a single run of the template generation, so is GUID(2) etc (but they are different to each other).

9.  For the times when you want to clone a git repo into a subfolder of a project, there is a special file name: **\_\_GITCLONE__**. 

    The file should contain a link to a repository on a single line, and nothing else (e.g. https:github.com/autotelic-sasha/autotelica_core.git).

    Then, during the template instantiation, the repo will be cloned into the directory containining the file. 
    This works by simple substitution: `git clone --depth=1 repo_name_from_the_file path_to_folder_where_the_file_is` .
    Obviously, you can hack it by adding git parameters to the file, e.g. --brach bname https:github.com/autotelic-sasha/autotelica_core.git .
    *Note*: .git folder gets renamed to .original_dot_git ... you can delete it, ignore it, or rename it to .git if you are github wizard.


## Where do the values for replacements come from?
     
When running this from a command line you can either supply names mapping on a command line or supply a path to a configuration file containing them. The configuration file can be json or ini.

The class that does all the work will take a `map<string, string>` as a constructor argument too, so you can use that if you are extending the funcionality for your own neffarious purposes.

The names can be scoped (it's handy if your templates become big), but only to one level. 
You do this by creating "sections", blocks with names that becomes first part of all the names defined in that section before a dot ... ok, ok, far easier to show you an example:
     
Say you created an ini file (say, config.ini) that looks like this:

    ; Comment about the meaning of it all
    blah = blahblah
    umm = pause
    [meaningfull]
    ; Some other thoughts about it all
    boom = bang
    all = love

Now the names get mapped like this:
         
    {{blah}} or __blah__ is replaced by blahblah
    {{umm}} or __umm__ is replaced by pause
    {{meaningfull.boom}} or __meaningfull.boom__ is replaced by bang
    {{meaningfull.all}} or __meaningfull.all__ is replaced by love

Equivalent JSON would look like this:

    {
        "sections" : [
            {
                "name" : "", 
                "named_values": [
                    { "name" : "blah", "value" : "blahblah" },
                    { "name" : "umm", "value" : "pause" }
                ]
            },
            {
                "name" : "meaningfull", 
                "named_values": [
                    { "name" : "boom", "value" : "bang" },
                    { "name" : "all", "value" : "love" }
                ]
            }
        ]
    }

*Hint:* if you don't need named sections, you can just use "named_values" block at the top level.

     		

## What else?

1. You can specify file extensions or file names to ignore.
   These are simply copied, possibly with name changes, but the content is not parsed. 
   Super handy when you have binary files, like Excel sheets or whatnot, in your templates.
   You can do this either on the command line or in the input files, just add values like:

         "extensions_to_ignore" : "xls,exe,so",
         "files_to_ignore" : "large_cpp.cpp, large_header.h"

   in json, or

         extensions_to_ignore = xls,exe,so
         files_to_ignore = large_cpp.cpp, large_header.h

   in ini files, or similarly on the command line.

    *Hints*
    1. files_to_ignore and extensions to ignore also work with wildcards (e.g. *part\of\path*)
    2. if a directory matches one of the listed names, everything in that directory is also not parsed. 
    3. names of files and directories are always parsed though

 3. If the same parameter appears both on a command line and in a config file, the command line version takes presedence.    

 4. There are examples in the `examples` folder.
