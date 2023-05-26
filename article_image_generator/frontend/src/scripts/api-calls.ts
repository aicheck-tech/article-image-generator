export async function textToImage(
        text: string, 
        image_look: string,
        processing_method: string,
        batch_size: number,
        ): Promise<{ images_base64: Array<string>; prompts: Array<string> }> {

    const request_body = {
        text_for_processing: text,
        image_look: image_look,
        samples: batch_size,
    };

    let request_url: string;
    if (processing_method === "Key-words") {
        request_url = "/backend/text-to-image/keywords";
    }
    else if (processing_method === "Summarization") {
        request_url = "/backend/text-to-image/summarization";
    }

    const request = new Request(request_url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(request_body),
    });

    const request_response = await fetch(request);
    const data = await request_response.json();
    console.log(data);
    return {
        prompts: data.prompt,
        images_base64: data.images_base64,
    };
}