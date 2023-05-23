export async function textToImage(text: string, image_look: string): Promise<{ image_base64: string; prompt: string; confidence: number; }> {
    const request_body = {
        text_for_processing: text,
        image_look: image_look
    };

    const request = new Request("/backend/text-to-image", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(request_body),
    });

    const request_response = await fetch(request);
    const data = await request_response.json();
    return {
        image_base64: data.image_base64,
        prompt: data.prompt,
        confidence: data.confidence
    };
}