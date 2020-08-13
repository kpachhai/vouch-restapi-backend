# -*- coding: utf-8 -*-

import base64
import json
import requests

from app import config


class DidRetrieval(object):

    def __init__(self, did):
        self.did = did

    def _resolve_did(self):
        payload = {
            "method": "resolvedid",
            "params": {
                "did": self.did,
                "all": False
            }
        }
        response = requests.post(config.DID_SIDECHAIN_RPC_URL, json=payload).json()
        return response

    def get_current_did_document(self):
        document = None
        response = self._resolve_did()
        if response["result"]:
            transactions = response["result"]["transaction"]
            if transactions:
                transaction = transactions[0]
                # Need to add some extra padding so TypeError is not thrown sometimes
                payload = base64.b64decode(transaction["operation"]["payload"] + "===").decode("utf-8")
                payload_json = json.loads(payload)

                verifiable_creds = []
                if "verifiableCredential" in payload_json.keys():
                    creds = payload_json["verifiableCredential"]
                    for cred in creds:
                        verifiable_cred = {
                            "id": cred["id"],
                            "issuance_date": cred["issuanceDate"],
                            "subject": cred["credentialSubject"],
                            "expiration_date": cred["expirationDate"],
                            "type": cred["type"]
                        }
                        if "issuer" in cred.keys():
                            verifiable_cred["issuer"] = cred["issuer"]
                        verifiable_creds.append(verifiable_cred)

                document = {
                    "txid": transaction["txid"],
                    "published": transaction["timestamp"],
                    "verifiable_creds": verifiable_creds
                }
        return document
