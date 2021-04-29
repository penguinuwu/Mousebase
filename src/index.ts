import axios from "axios";

async function getAuth(): Promise<{ access_token: string } | null> {
  try {
    // request for token
    const res = await axios({
      method: "post",
      url: "https://osu.ppy.sh/oauth/token",
      data: {
        grant_type: "client_credentials",
        client_id: Number(process.env.CLIENT_ID),
        client_secret: process.env.CLIENT_SECRET,
        scope: "public"
      }
    });
    return res.data;
  } catch (error) {
    console.error(error);
    return null;
  }
}

async function getUser(token: string, userID: string): Promise<any> {
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

async function main() {
  const token = await getAuth();
  if (!token || Object.keys(token).length === 0)
    return console.error("no token");

  const user = await getUser(token.access_token, "3607337");
  console.log(user["statistics"]);
  console.log(user["statistics"]["pp"]);
  console.log(user["statistics"]["global_rank"]);
}

main();
