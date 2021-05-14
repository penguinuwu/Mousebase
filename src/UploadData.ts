import fs from "fs";
import { getDB } from "./Utils";

function readJSON(filePath: string) {
  let rawData = fs.readFileSync(filePath);
  return JSON.parse(rawData.toString());
}

function uploadUsers() {
  const users = readJSON(`${process.env.USERS_JSON}`);
  const db = getDB();
  for (const user in users)
    db.collection("user").doc(user).set(users[user]).catch(console.error);
}

function uploadMice() {
  const mice = readJSON(`${process.env.MICE_JSON}`);
  const db = getDB();
  for (const m in mice)
    db.collection("mouse").doc(m).set(mice[m]).catch(console.error);
}

function uploadMousepads() {
  const mousepads = readJSON(`${process.env.MOUSEPADS_JSON}`);
  const db = getDB();
  for (const mp in mousepads)
    db.collection("mousepad").doc(mp).set(mousepads[mp]).catch(console.error);
}

function uploadKeyboards() {
  const keyboards = readJSON(`${process.env.KEYBOARDS_JSON}`);
  const db = getDB();
  for (const kb in keyboards)
    db.collection("keyboard").doc(kb).set(keyboards[kb]).catch(console.error);
}

uploadUsers();
uploadMice();
uploadMousepads();
uploadKeyboards();
