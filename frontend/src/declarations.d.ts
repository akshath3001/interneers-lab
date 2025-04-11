// done to inform TS that SVGs can be imported as strings(e.g. their file path)
declare module "*.svg" {
  const content: string;
  export default content;
}
