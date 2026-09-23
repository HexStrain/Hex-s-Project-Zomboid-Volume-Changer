# ⚙️ Hex's Project Zomboid Volume Customizer

Because of a hardcoded bug in Project Zomboid's FMOD audio engine, achieving perfect 2D audio (no weird left/right ear 3D panning) completely disables the game's ability to read Lua-based volume sliders. 

To bypass this and give you full control over how loud your death songs are, this tool permanently alters the physical loudness of the `.ogg` files themselves. 

## 📥 Prerequisites 

1. **Python:** You must have [Python installed](https://www.python.org/downloads/). *(Make sure to check the box that says "Add Python to PATH" during installation!)*
2. **FFmpeg:** The tool requires `ffmpeg.exe` to process the audio. 
   - Download the `ffmpeg.exe` file (you can find Windows builds [here](https://github.com/BtbN/FFmpeg-Builds/releases)).
   - **Place `ffmpeg.exe` in the exact same folder** as this Volume Changer script.

## 🚀 How to Use

1. Subscribe to the death song(s) you want on the Steam Workshop.
2. Run **`Run_VolumeChanger.bat`**.
3. Click **Browse**. **The tool will automatically locate your Project Zomboid Steam Workshop folder!** Just select the main folder of the mod you want to edit. *(It will also automatically scan through all internal subfolders to find the Build 41 and Build 42 audio files for you).*
4. Adjust the slider to your desired volume:
   * `-45`: Very quiet (Best for high-gain headphones).
   * `-27`: Normal (Default Zomboid audio baseline).
   * `-12`: Extremely loud.
5. Click **Apply Volume**.

> **💡 PRO TIP:** Don't launch the game to test the volume! Game engines lock audio files into memory while running. Instead, click the **"📁 Open Folder"** button to play the `.ogg` file in your standard Windows media player. You can quickly test and tweak the slider as many times as you need *before* booting up Project Zomboid!

### 🔄 Failsafe: Automatic Backups
The very first time you adjust a song's volume, the tool secretly creates a pristine backup of the original Steam file (saved safely inside the mod's `media/sound` folder as a `.bak` file). 
* If you adjust the volume multiple times, it always calculates the new audio from the pristine backup to ensure there is zero audio degradation or distortion.
* If you make a mistake or want the vanilla audio back, just click **"Restore Originals"** to instantly revert the mod to its original state.