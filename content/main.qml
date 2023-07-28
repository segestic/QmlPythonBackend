import QtQuick 2.12
import QtQuick.Controls 2.12

ApplicationWindow {
    visible: true
    width: 800
    height: 600
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
            console.log("Result from rfid connection function:", myRfidQml)
        }
    }

    // Define the frontend variable
    property int frontendVariable: 0

    // Call the backend function and display the result
    Button {
        id: button1
        width: 250
        height: 80
        anchors.left: parent.left
        anchors.leftMargin: 20
        anchors.top: parent.top
        anchors.topMargin: 20
        text: "Call Backend IP Function"
        onClicked: {
            var result = backend.backendFunction()
            console.log("Result from backend function:", result)
        }
    }

    Button {
        id: button2
        width: 250
        height: 80
        anchors.left: parent.left
        anchors.leftMargin: 20
        text: "Call Backend RFID Start"
        anchors.top: text3.bottom
        anchors.topMargin: 20
        onClicked: { rfidbackend.start_reading() }
    }

    Button {
        id: button3
        width: 250
        height: 80
        background: Rectangle {
            color: "red" // Change the color to any valid color
        }
        anchors.left: parent.left
        anchors.leftMargin: 20
        text: "Call Backend RFID Stop"
        anchors.top: text4.bottom
        anchors.topMargin: 20
        onClicked: {
           { rfidbackend.stop_reading() }
        }
    }

    Button {
        id: button4
        width: 250
        height: 80
        background: Rectangle {
            color: "yellow" // Change the color to any valid color
        }
        anchors.left: parent.left
        anchors.leftMargin: 20
        text: "Call Backend Antena On"
        anchors.top: button3.bottom
        anchors.topMargin: 20
        onClicked: {
           { rfidbackend.start_antenna() }
        }
    }


    // Display the frontend and backend variables
    Text {
        id: text1
        anchors.left: parent.left
        anchors.leftMargin: 20
        text: "Frontend Variable: " + frontendVariable
        anchors.top: button1.bottom
        anchors.topMargin: 20
    }

    Text {
        id: text2
        anchors.left: parent.left
        anchors.leftMargin: 20
        text: "Backend Variable: " + backend.backendVariable
        anchors.top: text1.bottom
        anchors.topMargin: 20
    }
    Text {
        id: text3
        anchors.left: parent.left
        anchors.leftMargin: 20
        text: "Backend IP: " + ipbackend.my_ip_address //+ ' ' + myIp
        anchors.top: text2.bottom
        anchors.topMargin: 20
    }
    Text {
        id: text4
        anchors.left: parent.left
        anchors.leftMargin: 20
        text: "Backend RFID: " + myRfidQml
        anchors.top: button2.bottom
        anchors.topMargin: 20
    }
}

