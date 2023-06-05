def conversation(classification):    
    if classification["class"] == "greeting":
        return greeting(classification["class"])
    elif classification["class"] == "notCharging":
        return vehicleChargingStatus(classification["class"])
    elif classification["class"] == "chargeCompletionTime":
        return vehicleChargeCompletionTime(classification["class"])
    else:
        return newQuery(classification["class"])

def greeting(input):
    return input

def vehicleChargingStatus(input):
    return input

def vehicleChargeCompletionTime(input):
    return input

def newQuery(input):
    return input

