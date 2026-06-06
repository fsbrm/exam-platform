@REM ----------------------------------------------------------------------------
@REM Maven Wrapper startup script
@REM ----------------------------------------------------------------------------
@echo off
set MAVEN_HOME=
set "MVNW_VERBOSE=false"

if not "%MAVEN_HOME%"=="" (
    set "M2_HOME=%MAVEN_HOME%"
)

for %%i in ("%CD%") do set "DIRNAME=%%~nxi"

set "MAVEN_PROJECTBASEDIR=%CD%"
if not "%MAVEN_PROJECTBASEDIR%"=="" goto endDetectBaseDir

:findBaseDir
set "MAVEN_PROJECTBASEDIR=%CD%"
cd "%MAVEN_PROJECTBASEDIR%"
goto endDetectBaseDir

:endDetectBaseDir
set "MAVEN_OPTS=-Xmx1024m"

if exist "%USERPROFILE%\.m2\wrapper\dists" (
    set "MVNW_REPOURL=file:///%USERPROFILE%/.m2/wrapper/dists"
)

IF "!MVNW_CLASSPATH!"=="" (
    for %%i in ("%CD%\.mvn\wrapper\maven-wrapper.jar") do set "MVNW_CLASSPATH=%%i"
)

set "MVNW_CMD=mvnw"
"%JAVA_HOME%\bin\java.exe" %MAVEN_OPTS% -classpath "%MVNW_CLASSPATH%" "-Dmaven.multiModuleProjectDirectory=%MAVEN_PROJECTBASEDIR%" org.apache.maven.wrapper.MavenWrapperMain %*
