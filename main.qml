import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: true
    width: 400
    height: 300
    title: qsTr("Backend Python")

    property string myIp: " "//String(ipbackend.ipAddress)

    // Create an instance of the backend
    Connections {
        target: backend

        // Receive the backend variable and update the frontend variable
        function onBackendVariableChanged() {
            frontendVariable += backend.backendVariable
        }
        //onBackendVariableChanged: frontendVariable = backend.backendVariable
    }
    Connections {
        target: ipbackend
        onIpAddressChanged: {
            myIp = ipbackend.my_ip_address
        }
    }


    // Define the frontend variable
    property int frontendVariable: 0

    // Call the backend function and display the result
    Button {
        id: button1
        text: "Call Backend Function"
        onClicked: {
            var result = backend.backendFunction()
            console.log("Result from backend function:", result)
        }
    }

    // Display the frontend and backend variables
    Text {
        id: text1
        text: "Frontend Variable: " + frontendVariable
        anchors.top: button1.bottom
        anchors.topMargin: 10
    }

    Text {
        id: text2
        text: "Backend Variable: " + backend.backendVariable
        anchors.top: text1.bottom
        anchors.topMargin: 10
    }
    Text {
        id: text3
        text: "Backend IP: " + ipbackend.my_ip_address //+ ' ' + myIp
        anchors.top: text2.bottom
        anchors.topMargin: 10
    }
}

