from os import getcwd
from requests import get
from json import dumps, load
from inquirer import List, Text, prompt
import inquirer as inq
from tqdm import tqdm
from websocket import create_connection
from const import welcomeMessage
from const import helpMessage

# -----------------------------------------------------------------------


class Result:
    def __init__(self, status, text) -> None:
        self.status = status
        self.text = text


# -----------------------------------------------------------------------


def main():
    # First Settings load
    settings = load_settings("settings.json")
    if settings is None:
        print("Setting load error")
        return

    ws_url = "ws://" + settings["ip_oscilloscope"] + ":5850/"
    # Open WebSocketConnection
    ws_connection = True
    # ws_connection = openWebSocketConnection(ws_url)
    if ws_connection == None:
        print("Ws Connection load error")
        return

    # turnOnOscilloscope(ws_connection, settings)

    print(welcomeMessage)

    while True:
        match getCommand():
            case "Change filename":
                # Retrieve the new file name
                question = [
                    Text(
                        "filename",
                        message="Enter the file name",
                    )
                ]
                filename = prompt(question)["filename"]

                settings["file_name"] = filename
                # Override the settings.json file with the new one
                result = write_settings(settings, "settings.json")
                if not result.status:
                    print(result.text)
                    return
                print("\n---- File saving name changed ----\n")

            case "Load settings":
                settings = load_settings("settings.json")
                if settings is None:
                    print("Setting load error")
                    return
                print("\n---- Setting loaded from settings.json ----\n")

            case "Change settings":
                for key in ["file_name", "n_acquisitions", "n_file"]:
                    # Retrieve the new key value
                    questions = [
                        Text(
                            "setting",
                            message=key,
                        )
                    ]
                    settings[key] = prompt(questions)["setting"]

                # Override the settings.json file with the new one
                result = write_settings(settings, "settings.json")
                if not result.status:
                    print(result.text)
                    return
                print("\n---- Settings saved ----\n")
            case "Read data":
                print("Reading data")
                result = readData(ws_connection, settings)
                if not result.status:
                    print(result.text)
                    return
                print("\n---- Reading completed ----\n")

            case "Help":
                print(helpMessage)
                input("Press enter to continue...")

            case "Exit":
                return

            case _:
                print("Command doesn't exists")


# -----------------------------------------------------------------------


def getCommand():
    options = [
        List(
            "command",
            message="What's your next command?",
            choices=[
                "Change filename",
                "Read data",
                "Change settings",
                "Load settings",
                "Help",
                "Exit",
            ],
        )
    ]
    return prompt(options)["command"]


# -----------------------------------------------------------------------


def write_settings(settings, file_name):
    try:
        file = open(file_name, "w")
        file.write(dumps(settings, indent=4))
        file.close()
        return Result(True, "")
    except:
        return Result(False, "Write settings error")


# -----------------------------------------------------------------------


def openWebSocketConnection(ws_url):
    try:
        ws = create_connection(ws_url, timeout=5)

        #    print("Sending 'Hello, World'...")
        #    ws = create_connection("ws://10.194.101.66:5850/")
        #    print(ws.recv())
        #
        #    ws.send(settings["activateOscilloscopeMessage"])
        #    print("Sent")
        #    print("Receiving...")
        #    # result = ws.recv()
        #    # print("Received '%s'" % result)
        #    ws.close()

        result = ws.recv()
        print(result)
        return ws
    except:
        return None


# -----------------------------------------------------------------------


def load_settings(file_name):
    try:
        file = open(file_name)
        settings = load(file)
        file.close()
        return settings
    except:
        return None


# -----------------------------------------------------------------------


def readData(ws_connection, settings):
    cwd = getcwd()
    for i in tqdm(range(1, int(settings["n_file"]) + 1)):
        # If only one file will be saved, enumeration is not necessary
        if settings["n_file"] == 1:
            file_name = f"{cwd}\\files\\{settings['file_name']}.csv"
        else:
            file_name = f"{cwd}\\files\\{settings['file_name']}_{str(i)}.csv"
        # Make CSV request
        result = csv_request(settings)
        if result is None:
            return Result(False, "CSV request timeout")

        # Make CSV file request
        result = file_request(settings)
        if result is None:
            return Result(False, "File request timeout")

        if not write_csv(result.text, file_name).status:
            return Result(False, "Write CSV Error")

        # if not turnOnOscilloscope(ws_connection, settings):
        #    return Result(False, "Turn On error")

    return Result(True, "")


# -----------------------------------------------------------------------


def write_csv(csv, file_name):
    try:
        file = open(file_name, "w")
        file.write(csv)
        file.close()
        return Result(True, "")
    except:
        return Result(False, "Write CSV error")


# -----------------------------------------------------------------------


def turnOnOscilloscope(ws, settings):
    ws.send(settings["activateOscilloscopeMessage"])
    result = ws.recv()
    print(result)
    return True


# -----------------------------------------------------------------------


def csv_request(settings):
    try:
        response = get(
            settings["url_csv"].format(
                settings["ip_oscilloscope"],
                settings["file_name"],
                settings["n_acquisitions"],
            ),
            timeout=5,
        )

        # response = requests.get(settings["url_csv"], timeout=5)

        return response
    except:
        return None


# -----------------------------------------------------------------------


def file_request(settings):
    try:
        response = get(
            settings["url_file"].format(
                settings["ip_oscilloscope"],
                settings["file_name"],
                settings["n_acquisitions"],
            ),
            timeout=5,
        )

        return response
    except:
        return None


# -----------------------------------------------------------------------

main()
