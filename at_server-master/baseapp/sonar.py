import json, re, requests, time

from django.conf import settings

host = settings.ONLINE_SONAR_HOST

class Sonar:
    @classmethod
    def get_sonar_result(cls, sonar_name, host=host):
        result = {}
        response = requests.get(
            f'{host}/api/measures/component?additionalFields=metrics%2Cperiods&component={sonar_name}&metricKeys=alert_status%2Cquality_gate_details%2Cbugs%2Cnew_bugs%2Creliability_rating%2Cnew_reliability_rating%2Cvulnerabilities%2Cnew_vulnerabilities%2Csecurity_rating%2Cnew_security_rating%2Ccode_smells%2Cnew_code_smells%2Csqale_rating%2Cnew_maintainability_rating%2Csqale_index%2Cnew_technical_debt%2Ccoverage%2Cnew_coverage%2Cnew_lines_to_cover%2Ctests%2Cduplicated_lines_density%2Cnew_duplicated_lines_density%2Cduplicated_blocks%2Cncloc%2Cncloc_language_distribution%2Cprojects%2Cnew_lines')
        for row in response.json().get('component').get('measures'):
            if row.get('metric') == 'bugs':
                result['bugs'] = row.get('value')
            if row.get('metric') == 'vulnerabilities':
                result['vulnerabilities'] = row.get('value')
            if row.get('metric') == 'ncloc':
                result['ncloc'] = row.get('value')
        return result


if __name__ == '__main__':
    print(time.time())
    Sonar.get_sonar_result("com.loanking:skynet-ship")
    print(time.time())
