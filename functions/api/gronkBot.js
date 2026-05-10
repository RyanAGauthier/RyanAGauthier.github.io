export async function onRequestPost(context) {
//Step 0: Check if request has required authentication
if (context.request.headers.has("X-Signature-Ed25519") && context.request.headers.has("X-Signature-Timestamp")){
    const temp_PUBLIC_KEY = context.env.D_PUBKEY;
    //Step 1: Convert the raw public key to a CryptoKey, https://developer.mozilla.org/en-US/docs/Web/API/CryptoKey
    const PUBLIC_KEY = await crypto.subtle.importKey('raw', Uint8Array.fromHex(temp_PUBLIC_KEY),
						{
							name: 'Ed25519',
						}, false,['verify']);
    //Step 2: Make everything into TypedArrays that can be fed into subtleCrypto.verify
    const temp_signature = context.request.headers.get("X-Signature-Ed25519");
    const signature = Uint8Array.fromHex(temp_signature);
    const temp_timestamp = context.request.headers.get("X-Signature-Timestamp");
    let encoder = new TextEncoder();
    const timestamp = encoder.encode(temp_timestamp);
    const temp_body = await context.request.text();
    const body = encoder.encode(temp_body);
    //Weird that I can set a const, but that's JS
    const data = new Uint8Array(timestamp.length + body.length);
    data.set(timestamp);
    data.set(body, timestamp.length);
    //Step 3: Call crypto.subtle.verify
    let isVerified = await crypto.subtle.verify({ "name": "Ed25519",},PUBLIC_KEY,signature,data);
    if (!isVerified) {
        console.log("Invalid request signature or crypto failed...");
        return new Response("Invalid request signature!",{status: 401});
    }else{
        console.log("Valid signature!!!!!");
        //Step 4: Actually handle a given request
        //Check type
        const checkType = JSON.parse(temp_body);
        console.log(checkType);
        if ("type" in checkType){
            if(checkType["type"] == 1){
                //It's just a ping, return pong
                    return Response.json({"type": 1});
            }
            else if(checkType["type"] == 2){
                // It's a valid interaction, do something
                if (checkType["data"]["name"] == "gronkisthistrue"){
                    console.log("gronk is this trued????");
                    let options = checkType["data"]["options"][0]["value"];
                    console.log(`Options: ${options}`);
                    const response = await env.LLM.run("@cf/google/gemma-4-26b-a4b-it", {
                        prompt: options,
                    });
                    return new Response(JSON.stringify(response));
                }
                return Response.json({type: 4, data: {content: "Hello, I'm Gronk. I'm a work in progress!"}});
            }
            else{
                console.log("Type present but supported, weird...");
                return new Response("Invalid type!", {status: 400});
            }
        }else{
            console.log("Missing type but still had auth headers...");
            return new Response("Missing 'type' header...", {status: 400});
        }
    }         
}else{
    return new Response("Missing headers...",{status: 401})
}
    //https://docs.discord.com/developers/interactions/overview#validating-security-headers
    //https://github.com/discord/discord-interactions-js/blob/main/src/index.ts

}