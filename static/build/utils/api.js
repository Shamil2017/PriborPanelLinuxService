export const sendData = async (data) => {
    const res = await fetch('/answer', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    });
    if (res.ok) {
        return Promise.resolve(`Success ${res.status}`);
    }
    throw new Error(`${res.status}`);
};
