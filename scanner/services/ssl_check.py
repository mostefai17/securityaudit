import datetime
import socket
import ssl
from cryptography import x509
from cryptography.hazmat.backends import default_backend


def analyze_certificate(cert_pem):
    cert_der = ssl.PEM_cert_to_DER_cert(cert_pem)
    cert = x509.load_der_x509_certificate(cert_der, default_backend())
    expiration_date = cert.not_valid_after.replace(tzinfo=datetime.timezone.utc)
    current_date = datetime.datetime.now(datetime.timezone.utc)
    time_diff = expiration_date - current_date
    time_remaining = time_diff.days

    return expiration_date, time_remaining


def runsslaudit(host):
    print("Running SSL Audit on", host)
    try:
        cert = ssl.get_server_certificate((host, 443))
        expiration_date, time_remaining = analyze_certificate(cert)

        if time_remaining <= 0:
            return {
                "status": "expired",
                "expiration_date": expiration_date.strftime("%Y-%m-%d"),
                "days_remaining": 0
            }
        elif time_remaining <= 30:
            return {
                "status": "warning",
                "expiration_date": expiration_date.strftime("%Y-%m-%d"),
                "days_remaining": time_remaining
            }
        else:
            return {
                "status": "valid",
                "expiration_date": expiration_date.strftime("%Y-%m-%d"),
                "days_remaining": time_remaining
            }
    except Exception as e:
        return f"Error occurred while auditing {host}: {e}"


if __name__ == "__main__":
    hostname = socket.gethostname()
    runsslaudit(hostname)