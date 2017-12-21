@echo off

rem Define a (local) name for the temporary file
setlocal
set temp="tmp.txt"

rem Copy the list of outdated modules to a text file
call pip list --outdated > %temp%

rem Process the text file to only contain module names
call python -c "m='\n'.join(map(lambda x: x.split()[0], open('%temp%', 'r').readlines())); open('%temp%', 'w').write(m)"

rem Pipe the file back to pip and install the modules
call pip install --upgrade -r %temp%

rem Delete the text file
del %temp%

rem Free the now-unnecessary variable for the filename
endlocal