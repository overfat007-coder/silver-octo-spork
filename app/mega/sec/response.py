"""Incident response action helpers."""


def block_ip(ip:str)->dict:
    return {"action":"block_ip","ip":ip,"status":"done"}
