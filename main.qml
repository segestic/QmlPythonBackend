import QtQuick 2.12
import QtQuick.Controls 2.12

ApplicationWindow {
    visible: true
    width: 400
    height: 300
    title: qsTr("Backend Python")

    property string myIp: " "//String(ipbackend.ipAddress)
    property string myRfidQml: " " //rfidbackend.my_rfid_address


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

    Connections {
        target: rfidbackend
        onRfidAddressChanged: {
            myRfidQml = rfidbackend.my_rfid_address
            console.log("Result from rfid connection function:", myRfid)
        }
    }

    // Define the frontend variable
    property int frontendVariable: 0

    // Call the backend function and display the result
    Button {
        id: button1
        text: "Call Backend IP Function"
        onClicked: {
            var result = backend.backendFunction()
            console.log("Result from backend function:", result)
        }
    }

    Button {
        id: button2
        text: "Call Backend RFID Start"
        anchors.top: text3.bottom
        anchors.topMargin: 10
        onClicked: {
            var result = rfidbackend.read_rfid()
            console.log("Result from backend function:", result)
        }
    }

    Button {
        id: button3
        text: "Call Backend RFID Stop"
        anchors.top: text4.bottom
        anchors.topMargin: 10
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
    Text {
        id: text4
        text: "Backend RFID: " + myRfidQml
        anchors.top: button2.bottom
        anchors.topMargin: 10
    }
}

