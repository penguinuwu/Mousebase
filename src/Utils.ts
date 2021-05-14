import axios from "axios";
import { Firestore } from "@google-cloud/firestore";

async function getAuth(): Promise<{ access_token: string } | null> {
  try {
    // request for token
    const res = await axios({
      method: "post",
      url: "https://osu.ppy.sh/oauth/token",
      data: {
        grant_type: "client_credentials",
        client_id: Number(process.env.OSU_CLIENT_ID),
        client_secret: process.env.OSU_CLIENT_SECRET,
        scope: "public"
      }
    });
    return res.data;
  } catch (error) {
    console.error(error);
    return null;
  }
}

async function getUserData(token: string, userID: string): Promise<any> {
  try {
    // request for user
    const res = await axios({
      method: "get",
      url: `https://osu.ppy.sh/api/v2/users/${userID}/osu?key=id`,
      headers: { Authorization: `Bearer ${token}` }
    });
    return res.data;
  } catch (error) {
    console.error(error);
    return null;
  }
}

function getDB(): Firestore {
  return new Firestore({
    projectId: process.env.GOOGLE_APPLICATION_ID,
    keyFilename: process.env.GOOGLE_APPLICATION_CREDENTIALS
  });
}

export { getAuth, getUserData, getDB };
