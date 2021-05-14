Mouse = {
  name: {
    sensor: String,
    switch: String,
    weight: Number,
    length: Number,
    width: Number,
    height: Number
  }
};

Mousepad = {
  name: {}
};

Keyboard = {
  /* idk how to identify kbs */
  name: {
    switch: String
  }
};

User = {
  id: {
    // controlled by script
    name: String,
    rank: Number,
    pp: Number,
    is_banned: Boolean,

    // manually set
    is_traitor: Boolean,
    playstyle: String /* e.g. Mouse/KB, Mouse Only */,
    dpi: Number,
    windows_sensitivity: Number /* integers from 1 to 11, e.g. 6 (for 6/11) */,
    windows_acceleration: Boolean,
    osu_multiplyer: Number /* e.g. 1.0 */,
    osu_raw: Boolean,
    screen_width: Number /* e.g. 1920 */,
    screen_height: Number /* e.g. 1080 */,
    polling: Number /* e.g. 500 */,
    area_width: Number /* e.g. 75 */,
    area_height: Number /* e.g. 56 */,

    // manually set with dropdown, references other tables
    mouse: String, // references Mouse PRIMARY KEY
    mousepad: String, // references Mousepad PRIMARY KEY
    keyboard: String // references Keyboard PRIMARY KEY
  }
};
