import { Actor } from "apify";
import { CheerioCrawler, sleep } from "crawlee";
await Actor.init();
// Initialize
const requestQueue = await Actor.openRequestQueue();

const baseUrl = "https://www.bbc.com/news";
// Enqueue start URL
await requestQueue.addRequest({
  url: baseUrl,
  userData: { label: "start" },
});

// Create function for assigning request label
const labelFunc = (label) => (request) => {
  request.userData = { label };
  return request;
};
// Map of selectors to extract and enqueue
const linkData = {
  start: {
    selector: ".gs-o-list-ui--top-no-border.nw-c-nav__wide-sections > li > a",
    label: "list",
  },
  list: {
    selector: "header > div > h3 > a",
    label: null,
  },
};

// Create the crawler
const crawler = new CheerioCrawler({
  maxRequestRetries: 2,
  maxConcurrency: 2,
  maxRequestsPerMinute: 10,
  requestHandlerTimeoutSecs: 2,
  requestQueue,
  useSessionPool: true,
  sessionPoolOptions: { maxPoolSize: 1 },
  persistCookiesPerSession: true,
  requestHandler: async ({ $, request, enqueueLinks}) => {
    // Navigation page
    const randomNumber = Math.floor(Math.random() * (1750 - 850 + 1)) + 850;
    await sleep(randomNumber);
    if (request.userData.label) {
      // Extract and enqueue all links
      const ld = linkData[request.userData.label];
      await enqueueLinks({
        baseUrl,
        requestQueue,
        selector: ld.selector,
        transformRequestFunction: labelFunc(ld.label),
      });
    } else {
      const url = request.url;
      const title = $("#main-heading").text().trim();

      const elementsBetweenLis = Array.from($("article").children()).filter(
        (node) => {
          if (
            typeof node.attribs.class !== "undefined" &&
            node.attribs.class.includes(
              "RichTextComponentWrapper"
            )
            ) {
              return node.name === "div";
          }
        }
      );
      const text = elementsBetweenLis
        .map((element) => $(element).text())
        .join(" ");

      const imgURL = $("picture > img.ssrcss-evoj7m-Image:eq(0)").attr("src");
      // Save the result
      await Actor.pushData({
        url: url,
        title: title,
        text: text,
        imgURL: imgURL,
      });
    }
  },
});

// Run the crawler
await crawler.run();

await Actor.exit();
