from datetime import datetime
from pathlib import Path
from typing import List
from report import make_report
import time
from sslyze import (
    Scanner,
    ServerScanRequest,
    SslyzeOutputAsJson,
    ServerNetworkLocation,
    ScanCommandAttemptStatusEnum,
    ServerScanStatusEnum,
    ServerScanResult,
    ServerScanResultAsJson,
    RobotScanResult,
    RobotScanResultEnum,
    HeartbleedScanResult,
    AllScanCommandsAttempts,
    CertificateInfoScanResult,

)

output=[]
from sslyze.errors import ServerHostnameCouldNotBeResolved
from sslyze.scanner.scan_command_attempt import ScanCommandAttempt


def _print_failed_scan_command_attempt(scan_command_attempt: ScanCommandAttempt) -> None:
    print(
        f"\nError when running ssl_2_0_cipher_suites: {scan_command_attempt.error_reason}:\n"
        f"{scan_command_attempt.error_trace}"
    )


def main() -> None:
    url = input("Enter the target URL: ")
    print("=> Starting the scans")
    start_time=time.time()
    date_scans_started = datetime.utcnow()

    # First create the scan requests for each server that we want to scan
    try:
        all_scan_requests = [
            ServerScanRequest(server_location=ServerNetworkLocation(hostname=url)),
        ]
    except ServerHostnameCouldNotBeResolved:
        # Handle bad input ie. invalid hostnames
        print("Error resolving the supplied hostnames")
        return

    # Then queue all the scans
    scanner = Scanner()
    scanner.queue_scans(all_scan_requests)

    # And retrieve and process the results for each server
    all_server_scan_results = []
    for server_scan_result in scanner.get_results():
        all_server_scan_results.append(server_scan_result)
        print(f"\n\n****Results for {server_scan_result.server_location.hostname}****")

        # Were we able to connect to the server and run the scan?
        if server_scan_result.scan_status == ServerScanStatusEnum.ERROR_NO_CONNECTIVITY:
            # No we weren't
            print(
                f"\nError: Could not connect to {server_scan_result.server_location.hostname}:"
                f" {server_scan_result.connectivity_error_trace}"
            )
            output.append(
                f"\nError: Could not connect to {server_scan_result.server_location.hostname}:"
                f" {server_scan_result.connectivity_error_trace}")
            continue

        # Since we were able to run the scan, scan_result is populated
        assert server_scan_result.scan_result

        output.append("Open SSL port is: " + str(server_scan_result.server_location.port))
        robot_attempt=server_scan_result.scan_result.robot
        if robot_attempt.status == ScanCommandAttemptStatusEnum.ERROR:
            # An error happened when this scan command was run
            _print_failed_scan_command_attempt(robot_attempt)
        elif robot_attempt.status == ScanCommandAttemptStatusEnum.COMPLETED:
            # This scan command was run successfully
            robot_result = robot_attempt.result
            print("\nAccepted results for ROBOT: ")
            output.append("\nAccepted results for ROBOT: ")
            if robot_result.robot_result == RobotScanResultEnum.NOT_VULNERABLE_NO_ORACLE:
                print("NOT_VULNERABLE_NO_ORACLE")
                output.append("NOT_VULNERABLE_NO_ORACLE")
            else:
                print(robot_result)
                output.append(robot_result)

        heartbleed_attempt=server_scan_result.scan_result.heartbleed
        if heartbleed_attempt.status == ScanCommandAttemptStatusEnum.ERROR:
            # An error happened when this scan command was run
            _print_failed_scan_command_attempt(heartbleed_attempt)
        elif heartbleed_attempt.status == ScanCommandAttemptStatusEnum.COMPLETED:
            # This scan command was run successfully
            heartbleed_result = heartbleed_attempt.result
            print("\nAccepted results for Heartbleed: ")
            output.append("\nAccepted results for Heartbleed: ")
            if heartbleed_result.is_vulnerable_to_heartbleed:
                print ("Heartbleed is vulnerable!")
                output.append("Heartbleed is vulnerable!")
            else:
                print("Heartbleed is not vulnerable!")
                output.append("Heartbleed is not vulnerable!")

        openssl_attempt = server_scan_result.scan_result.openssl_ccs_injection
        if openssl_attempt.status == ScanCommandAttemptStatusEnum.ERROR:
            # An error happened when this scan command was run
            _print_failed_scan_command_attempt(openssl_attempt)
        elif openssl_attempt.status == ScanCommandAttemptStatusEnum.COMPLETED:
            # This scan command was run successfully
            openssl_result = openssl_attempt.result
            print("\nAccepted results for OpenSSL: ")
            output.append("\nAccepted results for openssl: ")
            if openssl_result.is_vulnerable_to_ccs_injection:
                print("OpenSSL is vulnerable!")
                output.append("OpenSSL is vulnerable!")
            else:
                print("OpenSSL is not vulnerable!")
                output.append("OpenSSL is not vulnerable!")

        crime_attempt = server_scan_result.scan_result.tls_compression
        if crime_attempt.status == ScanCommandAttemptStatusEnum.ERROR:
            # An error happened when this scan command was run
            _print_failed_scan_command_attempt(crime_attempt)
        elif openssl_attempt.status == ScanCommandAttemptStatusEnum.COMPLETED:
            # This scan command was run successfully
            crime_result = crime_attempt.result
            print("\nAccepted results for CRIME: ")
            output.append("\nAccepted results for CRIME: ")
            if crime_result.supports_compression:
                print("CRIME is vulnerable!")
                output.append("CRIME is vulnerable!")
            else:
                print("CRIME is not vulnerable!")
                output.append("CRIME is not vulnerable!")

        fallback_attempt = server_scan_result.scan_result.tls_fallback_scsv
        if fallback_attempt.status == ScanCommandAttemptStatusEnum.ERROR:
            # An error happened when this scan command was run
            _print_failed_scan_command_attempt(fallback_attempt)
        elif openssl_attempt.status == ScanCommandAttemptStatusEnum.COMPLETED:
            # This scan command was run successfully
            fallback_result = fallback_attempt.result
            print("\nAccepted results for fallback: ")
            output.append("\nAccepted results for fallback: ")
            if fallback_result.supports_fallback_scsv:
                print("fallback is not vulnerable!")
                output.append("fallback is not vulnerable!")
            else:
                print("fallback is vulnerable!")
                output.append("fallback is vulnerable!")

        renegotiation_attempt = server_scan_result.scan_result.session_renegotiation
        if renegotiation_attempt.status == ScanCommandAttemptStatusEnum.ERROR:
            # An error happened when this scan command was run
            _print_failed_scan_command_attempt(renegotiation_attempt)
        elif openssl_attempt.status == ScanCommandAttemptStatusEnum.COMPLETED:
            # This scan command was run successfully
            renegotiation_result = renegotiation_attempt.result
            print("\nAccepted results for Insecure Renegotiation: ")
            output.append("\nAccepted results for Insecure Renegotiation: ")
            if renegotiation_result.supports_secure_renegotiation:
                print("Renegotiation is secure!")
                output.append("Renegotiation is secure!")
            else:
                print("Renegotiation is insecure!")
                output.append("Renegotiation is insecure!")

        ssl2_attempt = server_scan_result.scan_result.ssl_2_0_cipher_suites
        if ssl2_attempt.status == ScanCommandAttemptStatusEnum.ERROR:
            # An error happened when this scan command was run
            _print_failed_scan_command_attempt(ssl2_attempt)
        elif ssl2_attempt.status == ScanCommandAttemptStatusEnum.COMPLETED:
            # This scan command was run successfully
            ssl2_result = ssl2_attempt.result
            assert ssl2_result
            print("\nAccepted cipher suites for SSL 2.0:")
            output.append("\nAccepted cipher suites for SSL 2.0:")
            for accepted_cipher_suite in ssl2_result.accepted_cipher_suites:
                print(f"* {accepted_cipher_suite.cipher_suite.name}")
                output.append("\nAccepted cipher suites for SSL 2.0:")

        ssl3_attempt = server_scan_result.scan_result.ssl_3_0_cipher_suites
        if ssl3_attempt.status == ScanCommandAttemptStatusEnum.ERROR:
            # An error happened when this scan command was run
            _print_failed_scan_command_attempt(ssl3_attempt)
        elif ssl3_attempt.status == ScanCommandAttemptStatusEnum.COMPLETED:
            # This scan command was run successfully
            ssl3_result = ssl3_attempt.result
            assert ssl3_result
            print("\nAccepted cipher suites for SSL 3.0:")
            output.append("\nAccepted cipher suites for SSL 3.0:")
            for accepted_cipher_suite in ssl3_result.accepted_cipher_suites:
                print(f"* {accepted_cipher_suite.cipher_suite.name}")
                output.append(f"* {accepted_cipher_suite.cipher_suite.name}")

        # Process the result of the TLS 1.3 scan command
        tls1_3_attempt = server_scan_result.scan_result.tls_1_3_cipher_suites
        if tls1_3_attempt.status == ScanCommandAttemptStatusEnum.ERROR:
            _print_failed_scan_command_attempt(tls1_3_attempt)
        elif tls1_3_attempt.status == ScanCommandAttemptStatusEnum.COMPLETED:
            tls1_3_result = tls1_3_attempt.result
            assert tls1_3_result
            print("\nAccepted cipher suites for TLS 1.3:")
            output.append("\nAccepted cipher suites for TLS 1.3:")
            for accepted_cipher_suite in tls1_3_result.accepted_cipher_suites:
                print(f"* {accepted_cipher_suite.cipher_suite.name}")
                output.append(f"* {accepted_cipher_suite.cipher_suite.name}")

        # Process the result of the certificate info scan command
        certinfo_attempt = server_scan_result.scan_result.certificate_info
        if certinfo_attempt.status == ScanCommandAttemptStatusEnum.ERROR:
            _print_failed_scan_command_attempt(certinfo_attempt)
        elif certinfo_attempt.status == ScanCommandAttemptStatusEnum.COMPLETED:
            certinfo_result = certinfo_attempt.result
            assert certinfo_result
            print("\nLeaf certificates deployed:")
            output.append("\nLeaf certificates deployed:")
            for cert_deployment in certinfo_result.certificate_deployments:
                leaf_cert = cert_deployment.received_certificate_chain[0]
                print(
                    f"{leaf_cert.public_key().__class__.__name__}: {leaf_cert.subject.rfc4514_string()}"
                    f" (Serial: {leaf_cert.serial_number})"
                )
                output.append(
                    f"{leaf_cert.public_key().__class__.__name__}: {leaf_cert.subject.rfc4514_string()}"
                    f" (Serial: {leaf_cert.serial_number})"
                )

        end_time = time.time()
        execution_time = end_time - start_time
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        date = (f"Function executed in {execution_time:.6f} seconds on {current_date}")
        make_report("SSL/TLS Scanner", url, output, "ssl_report.pdf", date)


if __name__ == "__main__":
    main()