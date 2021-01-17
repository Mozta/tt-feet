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
            case 1:
                alertmsg = "Se detectó aumento en las variables. Tome precauciones.";
                break;
            case 2:
                alertmsg = "Se detectó una medición anómala. Se recomienda tomar un descanso del calzado.";
                break;
            case 3:
                alertmsg = "Se detectó aumento en las variables. Tome precauciones.";
                break;
            case 4:
                alertmsg = "Se detectó una medición anómala. Se recomienda tomar un descanso del calzado.";
                break;
            case 5:
                alertmsg = "Se detectó un posible objeto dentro del calzado.";
                break;
            case 6:
                alertmsg = "Se detectó un posible objeto dentro del calzado.";
                break;
            case 8:
                alertmsg = "Se detectó un posible objeto dentro del calzado.";
                break;
            case 9:
                alertmsg = "Se detectó un posible objeto dentro del calzado.";
                break;
            case 11:
                alertmsg = "Se detectó una medición anómala. Se recomienda tomar un descanso del calzado.";
                break;
            case 13:
                alertmsg = "Se detectó una medición anómala. Se recomienda tomar un descanso del calzado.";
                break;
            case 20:
                alertmsg = "Se detectó una medición anómala. Se recomienda tomar un descanso del calzado.";
                break;
            case 21:
                alertmsg = "Se detectó aumento en la temperatura. Tome precauciones.";
                break;
            case 22:
                alertmsg = "Se detectó una medición anómala. Se recomienda tomar un descanso del calzado.";
                break;
            case 24:
                alertmsg = "Se detectó disminución en la temperatura. Tome precauciones.";
                break;
            case 25:
                alertmsg = "Se detectó aumento en la humedad. Tome precauciones.";
                break;
            case 26:
                alertmsg = "Se detectó disminución en la humedad. Tome precauciones.";
                break;
            case 28:
                alertmsg = "Se detectó una medición fuera de rango. Revise el dispositivo.";
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