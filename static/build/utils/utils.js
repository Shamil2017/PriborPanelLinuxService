export const createImageList = (imageType, descriptions) => {
  const list = [];

  for (const key in descriptions) {
    const type = key.split('_')[0];

    list.push({
      type,
      src: `static/build/images/${imageType}/${key}.png`,
      description: descriptions[key],
      group:
        type === 'green' ? 0 : type === 'red' ? 1 : type === 'yellow' ? 2 : -1,
    });
  }

  return list;
};
