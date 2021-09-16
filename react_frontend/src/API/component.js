import axios from 'axios';

const baseURL = 'http://localhost:5000/';
// const data = [
//   {
//     id: 'lpdnet',
//     status: 'ready',
//     name: 'License Plate Detection',
//     email: 'z@stengineering.com',
//     phone: '123',
//     info: 'Automatic license plate recognition (ALPR) on stationary to fast-moving vehicles is one of the common intelligent video analytics applications for smart cities. Some of the common use cases include parking assistance systems, automated toll booths, vehicle registration and identification for delivery and logistics at ports, and medical supply transporting warehouses. \n\n Being able to do this in real time is key to servicing these markets to their full potential. Traditional techniques rely on specialized cameras and processing hardware, which is both expensive to deploy and difficult to maintain.',
//     cover:
//       'https://www.researchgate.net/profile/Zain-Masood-4/publication/315489495/figure/fig3/AS:900203120967681@1591636557193/Figure-shows-some-results-of-our-end-to-end-license-plate-detection-and-recognition.png'
//   },
//   {
//     id: '2d_body_pose',
//     status: 'ready',
//     email: 'a@stengineering.com',
//     phone: '123',
//     name: 'Body Pose (2D) Recognition',
//     info: 'Human pose estimation is a popular computer vision task of estimating key points on a person’s body such as eyes, arms, and legs. This can help classify a person’s actions, such as standing, sitting, walking, lying down, jumping, and so on. \n\n Understanding the context of what a person might be doing in a scene has broad application across a wide range of industries.In a retail setting, this information can be used to understand customer behavior, enhance security, and provide richer analytics.In healthcare, this can be used to monitor patients and alert medical personnel if the patient needs immediate attention.On a factory floor, human pose can be used to identify if proper safety protocols are being followed. \n \n In general, this is a reliable approach in applications that require understanding of human activity and commonly used as one of the key components in more complex tasks such as gesture, tracking, anomaly detection, and so on.',
//     cover: 'https://developer-blogs.nvidia.com/wp-content/uploads/2021/06/output-image.png'
//   },
//   {
//     id: 'border_control',
//     status: 'development',
//     email: 'a@stengineering.com',
//     phone: '123',
//     name: 'Border Control',
//     cover:
//       'https://cdn.shopify.com/s/files/1/0173/8204/7844/articles/2_df8b40bc-cd21-4c80-88df-74620e050dd7_1024x1024.jpg?v=1596750821'
//   },
//   {
//     id: 'chat_bot',
//     status: 'development',
//     email: 'a@stengineering.com',
//     phone: '123',
//     name: 'Chatbot',
//     cover: 'https://cdn.pixabay.com/photo/2016/12/11/21/37/whatsapp-1900453_960_720.png'
//   }
// ];

export function getModels(callback) {
  // api request
  axios
    .get(`${baseURL}/api/models/list`)
    .then((e) => {
      callback(e.data.models);
    })
    .catch(() => {
      callback('Endpoint inactive');
    });
}

export function getModelDetails(id, callback) {
  // api request
  axios
    .get(`${baseURL}/api/info/${id}`)
    .then((e) => {
      callback(e.data[id]);
    })
    .catch(() => {
      callback('Endpoint inactive');
    });
}

export function getAvailableDemo(id, callback) {
  axios
    .get(`${baseURL}/api/info/${id}`)
    .then((e) => {
      console.log(e.data[id].api);
      callback(e.data[id].api);
    })
    .catch(() => {
      callback('Endpoint inactive');
    });
}

export function sendGetRequest(endpoint, callback, config) {
  axios
    .get(baseURL + endpoint, config)
    .then((e) => {
      callback(e.data);
    })
    .catch(() => {
      callback('Endpoint inactive');
    });
}

export function sendPostRequest(endpoint, data, callback, config) {
  axios
    .post(baseURL + endpoint, data, config)
    .then((e) => {
      callback(e.data);
    })
    .catch(() => {
      callback('Endpoint inactive');
    });
}
