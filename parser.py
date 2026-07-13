import re

IP_REGEX = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
URL_REGEX = r'https?://[^\s<>"\']+'
DOMAIN_REGEX = r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b'
MD5_REGEX = r'\b[a-fA-F0-9]{32}\b'
SHA1_REGEX = r'\b[a-fA-F0-9]{40}\b'
SHA256_REGEX = r'\b[a-fA-F0-9]{64}\b'

def extract_iocs(text):
    return{
        "IPs": list(set(re.findall(IP_REGEX, text))),
        "URLs": list(set(re.findall(URL_REGEX, text))),
        "Domains": list(set(re.findall(DOMAIN_REGEX, text))),
        "MD5": list(set(re.findall(MD5_REGEX, text))),
        "SHA1": list(set(re.findall(SHA1_REGEX, text))),
        "SHA256": list(set(re.findall(SHA256_REGEX, text))),
    }