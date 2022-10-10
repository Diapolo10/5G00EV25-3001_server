"use strict";

// Fetches and prints out the root response

const room_id = `7b039c76-e656-454e-a97a-85e7490bade4`;

const url = `/api/v1/rooms/{room_id}`;

const getResponse = async url => {
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error(
            `An error has occurred; $(response.status)`
        );
    }

    const result = await response.json();
    return result;
}

const data = getResponse(url).catch(error => error.message);
console.log(data);
