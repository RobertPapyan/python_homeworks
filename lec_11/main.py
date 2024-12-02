import requests


BASE_URL = "https://jsonplaceholder.typicode.com/"

def filter_get_results(data):

    filtered_results = []
    for item in data:
        title_words = item['title'].split()
        body_lines = item['body'].split('\n')

        if len(title_words) <= 6 and len(body_lines) <= 3:
            filtered_results.append(item)

    return filtered_results


def make_api_calls():
    # GET request
    print("Performing GET request...")
    response = requests.get(BASE_URL + "posts")
    if response.status_code == 200:
        data = response.json()
        print("Original Results:", len(data))
        filtered_data = filter_get_results(data)
        print("Filtered Results:", len(filtered_data))
        for item in filtered_data:
            print(f"ID: {item['id']}, Title: {item['title']}, Body: {item['body']}\n")
    else:
        print("GET request failed with status code:", response.status_code)

    # POST request
    print("\nPerforming POST request...")
    post_data = {
        "title": "Test title",
        "body": "Test body",
        "userId": 777
    }
    response = requests.post(BASE_URL + "posts", json=post_data)
    if response.status_code == 201:
        print("POST request successful:", response.json())
    else:
        print("POST request failed with status code:", response.status_code)

    # PUT request
    print("\nPerforming PUT request...")
    put_data = {
        "id": 1,
        "title": "New title",
        "body": "New body",
        "userId": 1
    }
    response = requests.put(BASE_URL + "posts/1", json=put_data)
    if response.status_code == 200:
        print("PUT request successful:", response.json())
    else:
        print("PUT request failed with status code:", response.status_code)

    # DELETE request
    print("\nPerforming DELETE request...")
    response = requests.delete(BASE_URL + "posts/1")
    if response.status_code == 200:
        print("DELETE request successful. Status Code:", response.status_code)
    else:
        print("DELETE request failed with status code:", response.status_code)


if __name__ == "__main__":
    make_api_calls()
