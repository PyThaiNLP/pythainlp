def isThai(chr):
    cVal = ord(chr)
    if(cVal >= 3584 and cVal <= 3711):
        return True
    return False