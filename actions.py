


def hvac_action(pred_temp, setpoint, deadband):

    if pred_temp > setpoint + deadband:
        return "COOL_ON"
    elif pred_temp < setpoint - deadband:
        return "HEAT_ON"
    else:
        return "IDLE"