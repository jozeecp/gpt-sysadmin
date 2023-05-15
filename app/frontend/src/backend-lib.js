/*
This is the backend library used to make REST https calls
to the backend server.
*/
export class Backend {
    constructor() {
        this.url = 'http://localhost:5000/';
    }

    async confirm_step(task_id) {
        console.log("Confirming next step on task: ", task_id);
        const path = 'v1/tasks/' + task_id + '/confirm';
        const full_url = this.url + path;
        console.log("full_url", full_url);
        const requestOptions = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
        }

        let human_msg = '', machine_msg = '', host_msg = '';
        try {
            const response = await fetch(full_url, requestOptions);
            const data = await response.json();

            // Handle the response data here
            console.log("data:");
            console.log(data);
            
            // Get the last message from response:
            const messages = data['task']['messages'];
            const messageBeforeLast = messages[messages.length - 2];
            host_msg = messageBeforeLast['machine_msg'];
            const lastMessage = messages[messages.length - 1];
            human_msg = lastMessage['human_msg'];
            machine_msg = lastMessage['machine_msg'];

            console.log("human_msg", human_msg);
            console.log("machine_msg", machine_msg);
            console.log("host_msg", host_msg);
        } catch (error) {
            // Handle any errors here
            console.error('Error:', error);
        }

        return [human_msg, machine_msg, host_msg];
    }

    async create_task(task_description) {
        // Define the URL and request options
        const path = 'v1/tasks'
        const full_url = this.url + path;
        console.log("full_url", full_url);
        const requestOptions = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                engine: 'gpt-4',
                taskDescription: task_description,
                host_id: '13e378c7-2ee6-4fef-bf1b-1893c97beb3e',
                user: 'root',
                supervised: true
            })
        };

        // Make the REST call using the fetch function
        let human_msg = '', machine_msg = '', task_id = '';

        try {
            const response = await fetch(full_url, requestOptions);
            const data = await response.json();

            // Handle the response data here
            console.log("data:");
            console.log(data);
            
            // Get the last message from response:
            task_id = data['task']['taskId'];
            const messages = data['task']['messages'];
            const lastMessage = messages[messages.length - 1];
            human_msg = lastMessage['human_msg'];
            machine_msg = lastMessage['machine_msg'];

            // console.log("human_msg", human_msg);
            // console.log("machine_msg", machine_msg);
        } catch (error) {
            // Handle any errors here
            console.error('Error:', error);
        }

        return [human_msg, machine_msg, task_id];
    }
}

export default Backend;
