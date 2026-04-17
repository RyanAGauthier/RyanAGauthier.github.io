export async function onRequestPost(context) {
    try {
        const ps = context.env.COUNTERTABLE.prepare("UPDATE counter SET count = count + 1 WHERE counterID = 0");
        const returnValue = await stmt.run();
        return Response.json(returnValue);
    } catch (e) {
        console.error({message: e.message});
        returnValue = e.message;
        return Response.json(returnValue);
    }
}

