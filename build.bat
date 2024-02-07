"C:\Program Files\Microsoft Visual Studio\2022\Community\MSBuild\Current\Bin\MSBuild.exe" -m -p:Configuration=Release Fronter\Fronter.sln
copy Fronter\Release Release

:: Requires a virtual environment with pyinstaller package in the pyinstaller folder
pyinstaller\Scripts\pyinstaller.exe Stellarior\Source\main.py --onefile
copy dist\main.exe Release\Stellarior
xcopy Stellarior\Data_Files\blankMod\ Release\Stellarior\blankMod\ /E /Y

python build.py
pause