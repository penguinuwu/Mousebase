import { getAuth, getUserData, getDB } from "./Utils";

async function updateRanks() {
  // get osu token
  const token = await getAuth();
  if (!token || Object.keys(token).length === 0)
    return console.error("no token");

  // connect to db
  const db = getDB();

  // get users
  const users = await db.collection("user").get();

  // update rank
  users.forEach(async (user) => {
    // get data in the form of
    // https://osu.ppy.sh/docs/index.html?javascript#user
    const userData = await getUserData(token.access_token, user.id);

    // no need to await for set data
    if (!userData) {
      // if data does not exist, this player is probably banned
      user.ref.update({
        is_banned: true,
        pp: 0,
        rank: null
      });
    } else {
      // update user name, pp, rank
      user.ref.update({
        is_banned: false,
        name: `${userData["username"]}`,
        pp: parseInt(userData["statistics"]["pp"]) || 0,
        rank: parseInt(userData["statistics"]["global_rank"]) || null
      });
    }
  });
}

// update ranks every certain amount of minutes
const intervalMinutes = 15;
setInterval(updateRanks, 1000 * 60 * intervalMinutes);

// immediately update ranks
updateRanks();
