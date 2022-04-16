export const capitalizeWord = (str: string) =>
  str.toLowerCase().replace(/\b\w/g, (l) => l.toUpperCase());
