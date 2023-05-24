import React, { useState, useEffect } from 'react';
import axios from 'axios';

export default function HostManager() {
    const [hostname, setHostname] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [ip_address, setIpAddress] = useState('');
    const [description, setDescription] = useState('');
    const [hosts, setHosts] = useState([]);
    const [selectedHostId, setSelectedHostId] = useState(null);

    const baseUrl = 'http://localhost:5000';

    useEffect(() => {
        // Fetch hosts from backend when the component mounts
        const path = '/v1/hosts';
        axios.get(baseUrl + path)
            .then(response => {
                setHosts(response.data);
                console.log('Hosts fetched:', response.data);
            })
            .catch(error => {
                console.error('Error fetching hosts:', error);
            });
    }, []);

    const registerHost = () => {
        // Post new host to backend
        const path = '/v1/hosts';
        axios.post(baseUrl + path, { 
            hostname,
            username,
            password,
            ip_address,
            description
        })
            .then(response => {
                // Update hosts with new host from backend
                setHosts(oldHosts => [...oldHosts, response.data]);
                setHostname('');
                setUsername('');
                setPassword('');
                setIpAddress('');
                setDescription('');
            })
            .catch(error => {
                console.error('Error registering host:', error);
            });
    };

    const handleHostSelect = (hostId) => {
        // Here you could do something when a host is selected
        console.log(`Selected host with id ${hostId}`);
        global.HOST_ID = hostId;
        console.log("global.HOST_ID: ", global.HOST_ID);
        setSelectedHostId(hostId);
    };

    return (
        <div
            style={{padding: '20px'}}
        >
            <h2>Register Host</h2>
            <div>
                <input
                    placeholder="Hostname"
                    value={hostname}
                    onChange={e => setHostname(e.target.value)}
                />
            </div>
            <div>
                <input
                    placeholder="Username"
                    value={username}
                    onChange={e => setUsername(e.target.value)}
                />
            </div>
            <div>
                <input
                    placeholder="Password"
                    value={password}
                    onChange={e => setPassword(e.target.value)}
                />
            </div>
            <div>
                <input
                    placeholder="IP Address"
                    value={ip_address}
                    onChange={e => setIpAddress(e.target.value)}
                />
            </div>
            <div>
                <input
                    placeholder="Description"
                    value={description}
                    onChange={e => setDescription(e.target.value)}
                />
            </div>
            <div>
                <button onClick={registerHost}>Register Host</button>
            </div>

            <h2>Select Host</h2>
            {hosts.map(host => (
                <div 
                    key={host.host_id} 
                    style={{
                        backgroundColor: host.host_id === selectedHostId ? 'lightgray' : 'transparent',
                        color: host.host_id === selectedHostId ? 'black' : 'lightgray',
                    }}
                    onClick={() => handleHostSelect(host.host_id)}
                >
                    {host.hostname} ({host.username})
                </div>
            ))}
        </div>
    );
}
