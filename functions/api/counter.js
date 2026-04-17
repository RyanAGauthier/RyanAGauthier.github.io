export async function onRequestGet(context) {
    try {
        const ps = context.env.COUNTERTABLE.prepare("Select count FROM counter WHERE counterID = 0");
        const returnValue = await ps.run();
        return Response.json(returnValue);
    } catch (e) {
        console.error({message: e.message});
        returnValue = e.message;
        return Response.json(returnValue);
    }
}

