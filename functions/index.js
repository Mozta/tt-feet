const functions = require('firebase-functions');
//import firebase admin SDK
const admin = require('firebase-admin');
const { messaging } = require('firebase-admin');
admin.initializeApp(functions.config().firebase);


// // Create and Deploy Your First Cloud Functions
// // https://firebase.google.com/docs/functions/write-firebase-functions
//
// exports.helloWorld = functions.https.onRequest((request, response) => {
//   functions.logger.info("Hello logs!", {structuredData: true});
//   response.send("Hello from Firebase!");
// });

exports.sendNotificationToFCMToken = functions.firestore.document('messages/{mUid}').onWrite(async (event) => {
    let uid = event.after.get('userUid');
    let cmsj = event.after.get('cmsj');
    //let content = event.after.get('content');
    let userDoc =  await admin.firestore().doc(`TTInsole/users/${uid}/fcm`).get();
    let fcmToken = userDoc.get('fcm');

    setmsg(cmsj);

    function setmsg(codemsg){
        switch (codemsg){
            case 0:
                alertmsg = "alerta 0";
                break;
            case 1:
                alertmsg = "alerta 1";
                break;
            case 2:
                alertmsg = "alerta 2";
                break;
            default:
                alertmsg = "error desconocido"
        }
    }


    var message = {
        notification: {
            title: "Diafeetis Notification",
            body: alertmsg,
        },
        token: fcmToken,
    }

    let response = await admin.messaging().send(message);
    console.log(response);
});