export default defineEventHandler(() => {
  const message = 'Hello, world!';
  const timestamp = new Date().toISOString();
  const thisIsCool = true;

  if (!thisIsCool) {
    throw createError({ status: 400, message: 'Error 400' });
  }

  return { message, timestamp, thisIsCool };
});
