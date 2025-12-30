const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;
let pythonProcess;

function createWindow() {
  mainWindow = new BrowserWindow({ 
    width: 1000, 
    height: 700,
    webPreferences: {
        nodeIntegration: true
    }
  });

  // POINT TO NEW UI PATH
  mainWindow.loadFile(path.join(__dirname, 'src', 'ui', 'index.html'));
}

function startPython() {
  // POINT TO NEW BACKEND PATH
  // Note: On Windows, use backslashes or path.join safety
  let pythonExecutable;

    if (app.isPackaged) {
      // PROD MODE: Look inside the resources/backend-dist folder we defined in package.json
      // path.join(process.resourcesPath, 'backend-dist', 'api.exe')
      pythonExecutable = path.join(process.resourcesPath, 'backend-dist', 'api.exe');
    } else {
      // DEV MODE: Look for the python inside venv
      pythonExecutable = path.join(__dirname, 'venv', 'Scripts', 'python.exe');
    }

    const apiScript = path.join(__dirname, 'src', 'backend', 'main.py');

    console.log("🚀 Starting Python from:", pythonExecutable);

    if (app.isPackaged) {
      // In prod, we just run the exe (no arguments needed)
      pythonProcess = spawn(pythonExecutable);
    } else {
      // In dev, we run python.exe and pass the script as an argument
      pythonProcess = spawn(pythonExecutable, [apiScript]);
    }

  pythonProcess.stdout.on('data', (data) => console.log(`Python: ${data}`));
  pythonProcess.stderr.on('data', (data) => console.error(`Python Error: ${data}`));
}

app.whenReady().then(() => {
  startPython();
  createWindow();
});

app.on('will-quit', () => {
  if (pythonProcess) pythonProcess.kill();
});