/* Instructor-provided serial reference. Do not modify. */

static inline int fractalIterate(float cRe, float cIm, int count)
{
    float zRe = cRe;
    float zIm = cIm;

    for (int i = 0; i < count; ++i) {
        if (zRe*zRe + zIm*zIm > 4.0f)
            return i;

        float re2 = zRe*zRe;
        float im2 = zIm*zIm;

        float newRe = zRe * (re2 - 3.0f*im2);
        float newIm = zIm * (3.0f*re2 - im2);

        zRe = cRe + newRe;
        zIm = cIm + newIm;
    }
    return count;
}

void fractalSerial(
    float x0, float y0, float x1, float y1,
    int width, int height,
    int startRow, int totalRows,
    int maxIterations,
    int output[])
{
    const float dx = (x1-x0) / static_cast<float>(width);
    const float dy = (y1-y0) / static_cast<float>(height);

    for (int row = startRow; row < startRow + totalRows; ++row) {
        const float y = y0 + row*dy;

        for (int col = 0; col < width; ++col) {
            const float x = x0 + col*dx;
            output[row*width + col] =
                fractalIterate(x, y, maxIterations);
        }
    }
}
