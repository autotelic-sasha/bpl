setlocal
call "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat
msbuild bpl.sln /p:Configuration=Debug
msbuild bpl.sln /p:Configuration=Release
endlocal