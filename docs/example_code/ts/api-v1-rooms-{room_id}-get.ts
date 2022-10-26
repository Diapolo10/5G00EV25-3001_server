/**
 * Fetch a room by ID from the API
 */

import fetch from 'node-fetch';

type Room = {
  id: number;
  name: string;
  public: boolean;
  owner: string | null;
};

type GetRoomResponse = {
  data: Room;
};

const room_id: string = "c6bcc4a2-0b1d-453b-8ca0-00634ece4867";

async function getRoomByID() {
  try {
    const response = await fetch(`localhost:11037/api/v1/rooms/${room_id}`, {
      method: 'GET',
      headers: {
        Accept: 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`Error! status: ${response.status}`);
    }

    const result = (await response.json()) as GetRoomResponse;

    console.log('result is: ', JSON.stringify(result, null, 4));

    return result;
  } catch (error) {
    if (error instanceof Error) {
      console.log('error message: ', error.message);
      return error.message;
    } else {
      console.log('unexpected error: ', error);
      return 'An unexpected error occurred';
    }
  }
}

getRoomByID();
