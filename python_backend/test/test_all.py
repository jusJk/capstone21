import requests
import docker

BASE_URL = "http://localhost:5000"
LPD_US_URL = "/api/lpdnet/internal"
LPD_EU_URL = "/api/lpdnet/neil"
LPR_US_URL = "/api/lprnet/internal"
LPR_EU_URL = "/api/lprnet/neil"
LPDLPR_URL = "/api/lpdlprnet/internal"
BPNET_URL = "/api/bpnet/internal"
TCNET_URL = "/api/tcnet/internal"

# def get_docker_ip():
#     client = docker.DockerClient()
#     container = client.containers.get("python-backend")
#     print('HI')
#     print(container.attrs['NetworkSettings'])
#     return container.attrs['NetworkSettings']['IPAddress']

# def is_responsive(url):
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             return True
#     except ConnectionError:
#         return False

# @pytest.fixture(scope="session")
# def docker_compose_file(pytestconfig):
#     return os.path.join(str(pytestconfig.rootdir), "../../", "docker-compose.yml")

# @pytest.fixture(scope="session")
# def http_service(docker_ip, docker_services):
#     """Ensure that HTTP service is up and responsive."""

#     # `port_for` takes a container port and returns the corresponding host port
#     port = docker_services.port_for("python-backend", 5000)
#     url = "http://{}:{}".format(docker_ip, port)
#     print(url)
#     return url

# def test_status_code(http_service):
#     status = 200
#     response = requests.get(http_service + "/api/lpdnet/internal")

#     assert response.status_code == status

## Get Tests
def test_lpr_eu_get():
    response_lpr = requests.get(BASE_URL + LPR_EU_URL)
    assert response_lpr.status_code == 200

def test_lpr_us_get():
    response_lpr = requests.get(BASE_URL + LPR_US_URL)
    assert response_lpr.status_code == 200

def test_lpd_eu_get():
    response_lpd = requests.get(BASE_URL + LPD_EU_URL)
    assert response_lpd.status_code == 200

def test_lpd_us_get():
    response_lpd = requests.get(BASE_URL + LPD_US_URL)
    assert response_lpd.status_code == 200

def test_lpdlpr_get():
    response_lpdlpr = requests.get(BASE_URL + LPDLPR_URL)
    assert response_lpdlpr.status_code == 200

def test_bpnet_get():
    response_bpnet = requests.get(BASE_URL + BPNET_URL)
    assert response_bpnet.status_code == 200

def test_tcnet_get():
    response_tcnet = requests.get(BASE_URL + TCNET_URL)
    assert response_tcnet.status_code == 200

## Post Tests
def test_lpr_us_post():
    fname_1 = 'ca286.png'
    fname_2 = 'wy963.png'
    request_files=[ ('image',(fname_1,open("lpr/"+fname_1,'rb'),'image/jpeg')) , ('image',(fname_2,open("lpr/"+fname_2,'rb'),'image/jpeg'))]
    headers = {}
    payload = {'filename':[fname_1, fname_2]}
    response = requests.post(BASE_URL + LPR_US_URL,
        headers=headers, 
        data=payload, 
        files=request_files)
    assert response.status_code == 200
    body = response.json()
    assert body['0']['license_plate'] == "5VCF203"
    assert body['1']['license_plate'] == "4339C"

def test_lpr_eu_post():
    fname_1 = 'test_077.jpg'
    fname_2 = 'eu10.jpg'
    request_files=[ ('image',(fname_1,open("lpr/"+fname_1,'rb'),'image/jpeg')) , ('image',(fname_2,open("lpr/"+fname_2,'rb'),'image/jpeg'))]
    headers = {}
    payload = {'filename':[fname_1, fname_2]}
    response = requests.post(BASE_URL + LPR_US_URL,
        headers=headers, 
        data=payload, 
        files=request_files)
    assert response.status_code == 200
    body = response.json()
    assert body['1']['license_plate'] == "RK735AS"
    assert body['0']['license_plate'] == "WA56660"

def test_lpd_us_post():
    fname_1 = 'cal-cp-6.jpg'
    fname_2 = 'two-cars-2.jpg'
    request_files=[ ('image',(fname_1,open("lpd/"+fname_1,'rb'),'image/jpeg')) , ('image',(fname_2,open("lpd/"+fname_2,'rb'),'image/jpeg'))]
    headers = {}
    payload = {'filename':[fname_1, fname_2]}
    response = requests.post(BASE_URL + LPD_US_URL,
        headers=headers, 
        data=payload, 
        files=request_files)
    assert response.status_code == 200
    body = response.json()
    assert len(body['0']['all_bboxes']) == 1
    assert len(body['1']['all_bboxes']) == 2

def test_lpd_eu_post():
    fname = 'eu11.jpg'
    request_files=[('image',(fname,open("lpd/"+fname,'rb'),'image/jpeg'))]
    headers = {}
    payload = {'filename':[fname]}
    response = requests.post(BASE_URL + LPD_US_URL,
        headers=headers, 
        data=payload, 
        files=request_files)
    assert response.status_code == 200
    body = response.json()
    assert len(body['0']['all_bboxes']) == 1

def test_bpnet_post():
    fname = 'bp-sample.png'
    request_files=[('image',(fname,open("bodyposenet/"+fname,'rb'),'image/jpeg'))]
    headers = {}
    payload = {'filename':[fname]}
    response = requests.post(BASE_URL + BPNET_URL,
        headers=headers, 
        data=payload, 
        files=request_files)
    assert response.status_code == 200
    body = response.json()
    assert len(body['bp-sample.png']) == 4

def test_lpdlprnet_post():
    fname = 'cal-cp-6.jpg'
    request_files=[('image',(fname,open("lpd/"+fname,'rb'),'image/jpeg'))]
    headers = {}
    payload = {'filename':[fname]}
    response = requests.post(BASE_URL + LPDLPR_URL,
        headers=headers, 
        data=payload, 
        files=request_files)
    assert response.status_code == 200
    body = response.json()
    assert len(body['0']['all_bboxes'] ) == 1
    assert body['0']['0_lpr']['license_plate'] == '6TNB642'

def test_tcnet_post():
    fname_1 = 'cal-cp-5.jpg'
    fname_2 = 'two-cars-2.jpg'
    request_files=[ ('image',(fname_1,open("lpd/"+fname_1,'rb'),'image/jpeg')) , ('image',(fname_2,open("lpd/"+fname_2,'rb'),'image/jpeg'))]
    headers = {}
    payload = {'filename':[fname_1, fname_2]}
    response = requests.post(BASE_URL + TCNET_URL,
        headers=headers, 
        data=payload, 
        files=request_files)
    assert response.status_code == 200
    body = response.json()
    assert len(body['0']['all_bboxes']) == 1
    assert len(body['1']['all_bboxes']) >= 2

if __name__ == "__main__":
    test_tcnet_post()