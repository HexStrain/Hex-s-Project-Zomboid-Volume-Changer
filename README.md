# ⚙️ Hex's Project Zomboid Volume Customizer

Because of a hardcoded bug in Project Zomboid's FMOD audio engine, achieving perfect 2D audio (no weird left/right ear 3D panning) completely disables the game's ability to read Lua-based volume sliders. 

To bypass this and give you full control over how loud your death songs are, this tool permanently alters the physical loudness of the `.ogg` files themselves. 

## 📥 Prerequisites 

You need Python and FFmpeg installed on your computer. You can install both instantly using the Windows Command Prompt.

**The Quick Install (Recommended):**
1. Click your Windows Start button, type `cmd`, right-click **Command Prompt**, and select **Run as administrator**.
2. Copy and paste this command and press Enter to install Python:
   `winget install Python.Python.3.12`
3. Copy and paste this command and press Enter to install FFmpeg:
   `winget install Gyan.FFmpeg`
4. *Restart your computer* if Windows doesn't register the new system paths.

*(If you prefer not to use the command line, you can download [Python here](https://www.python.org/downloads/) and manually place [FFmpeg](https://github.com/BtbN/FFmpeg-Builds/releases) inside this tool's folder).*

## 🚀 How to Use

1. Subscribe to the death song(s) you want on the Steam Workshop.
2. **Download this tool** (Click the green `<> Code` button at the top of this page -> **Download ZIP**) and **extract/unpack** the folder to anywhere on your computer. 
3. Open the extracted folder and double-click **`Run_VolumeChanger.bat`**.
4. Click **Browse**. **The tool will automatically locate your Project Zomboid Steam Workshop folder!** Just select the main folder of the mod you want to edit. *(It will automatically scan through all internal subfolders to find the Build 41 and Build 42 audio files for you).*
5. Adjust the slider to your desired volume:
   * `-45`: Very quiet (Best for high-gain headphones).
   * `-28`: Normal (Default Zomboid audio baseline).
   * `-12`: Extremely loud.
6. Click **Apply Volume**.

> **💡 PRO TIP:** Don't launch the game to test the volume! Game engines lock audio files into memory while running. Instead, click the **"📁 Open Folder"** button to play the `.ogg` file in your standard Windows media player. You can quickly test and tweak the slider as many times as you need *before* booting up Project Zomboid!

### 🔄 Failsafe: Automatic Backups
The very first time you adjust a song's volume, the tool secretly creates a pristine backup of the original Steam file (saved safely inside the mod's `media/sound` folder as a `.bak` file). 
* If you adjust the volume multiple times, it always calculates the new audio from the pristine backup to ensure there is zero audio degradation or distortion.
* If you make a mistake or want the vanilla audio back, just click **"Restore Originals"** to instantly revert the mod to its original state.
