/*
This is the backend library used to make REST https calls 
to the backend server.
*/
export class Backend {
    create_task(task_description) {
        // Define the URL and request options
        const url = 'http://backend:5000/v1/tasks';
        const requestOptions = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                engine: 'gpt-3.5-turbo',
                taskDescription: 'task_description',
                host: '13e378c7-2ee6-4fef-bf1b-1893c97beb3e',
                user: 'root',
                supervised: true,
                engine: 'gpt-3.5-turbo'
            })
        };

        // Make the REST call using the fetch function
        let response =  fetch(url, requestOptions)
            .then(response => response.json())
            .then(data => {
                // Handle the response data here
                console.log(data);
            })
            .catch(error => {
                // Handle any errors here
                console.error('Error:', error);
            });

        console.log(response);

        // get last message from response:
        // response['body']['task']['messages'][-1]['human_msg']
        let human_msg = response['body']['task']['messages'][-2]['human_msg']
        let machine_msg = response['body']['task']['messages'][-2]['machine_msg']
        console.log(human_msg);
        console.log(machine_msg);

        return [human_msg, machine_msg];
    }
}

export default Backend;
